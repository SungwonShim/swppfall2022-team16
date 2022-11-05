from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

import json

from bridgeUS.models import CustomUser, UserShop, ShopItem, ShopItemDetail, Review, Comment

def signup(request):
    if request.method == 'POST':
        req_data = json.loads(request.body.decode())
        username = req_data['username']    
        nickname = req_data['nickname']
        password = req_data['password']

        created_user = CustomUser.objects.create_user(username=username, nickname=nickname, password=password)

        # create default usershopmodel
        usershop = UserShop(user=created_user)

        usershop.save()
        
        return HttpResponse(status=201)
    else:
        return HttpResponseNotAllowed(['POST'])

@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])

def signin(request):
    if request.method == 'POST':
        req_data = json.loads(request.body.decode())
        username = req_data['username']
        password = req_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)            
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponseNotAllowed(['POST'])    

def signout(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    logout(request)
    return HttpResponse(status=204)

def usershop(request, user_id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    
    if not User.objects.filter(id=user_id).exists():
        return HttpResponse(status=404)

    user = User.objects.first(id=user_id)    

    if not UserShop.objects.filter(user=user).exists():
        return HttpResponse(status=404)

    usershop = UserShop.objects.filter(user=user).first()    

    response_dict = { 'id' : usershop.id, 'favorite_clothes' : usershop.favorite_clothes, 'credit' : usershop.credit, 'cart' : usershop.cart , 'purchased_item' : usershop.purchased_item }
    return JsonResponse(response_dict, safe=False, status=200)

def shopitemlist(request):
    if request.method != 'GET' and request.method != 'POST':
        return HttpResponseNotAllowed(['GET', 'POST'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if request.method == 'GET':
        if ShopItem.objects.count() <= 0:
            return JsonResponse([{}], safe=False, status=204)

        shopitem_all_list = [{ 'seller' : shopitem.seller.id, 'price' : shopitem.price, 'rating': shopitem.rating, 'star' : shopitem.star, 'type' : shopitem.type } 
        for shopitem in ShopItem.objects.all()]
    
        return JsonResponse(shopitem_all_list, safe=False, status=200)
    else:
        body = request.body.decode()
        shopitem_price = json.loads(body)['price']
        shopitem_type = json.loads(body)['type']
        shopitem_seller = request.user

        shopitem = ShopItem(seller=shopitem_seller, price=shopitem_price, type=shopitem_type)

        shopitem.save()
        
        response_dict = {'id': shopitem.id, 'seller' : shopitem.seller.id, 'price' : shopitem.price, 'rating': shopitem.rating, 'star': shopitem.star, 'type': shopitem.type }
        return JsonResponse(response_dict, status=201)
    

def shopitem(request, item_id):
    if request.method != 'GET' and request.method != 'PUT' and request.method != 'DELETE':
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if not ShopItem.objects.filter(id=item_id).exists():
        return HttpResponse(status=404)

    shopitem = ShopItem.objects.get(id=item_id)

    if shopitem.seller.id != request.user.id and (request.method == 'PUT' or request.method == 'DELETE'):
        return HttpResponse(status=403)

    if request.method == 'GET':
        response_dict = { 'id': shopitem.id, 'seller' : shopitem.seller.id ,'price' : shopitem.price, 'rating': shopitem.rating, 'star': shopitem.star, 'type': shopitem.type }
        return JsonResponse(response_dict, status=200)
    elif request.method == 'PUT':
        body = request.body.decode()

        shopitem_star = json.loads(body)['star']
        shopitem_rating = json.loads(body)['rating']
        shopitem_price = json.loads(body)['price']
        shopitem_type = json.loads(body)['type']


        shopitem.star = shopitem_star
        shopitem.rating = shopitem_rating
        shopitem.price = shopitem_price
        shopitem.type = shopitem_type

        shopitem.save()

        response_dict = { 'id': shopitem.id, 'seller' : shopitem.seller.id, 'price' : shopitem.price, 'rating': shopitem.rating, 'star': shopitem.star, 'type': shopitem.type }
        return JsonResponse(response_dict, status=200)
    else:
        shopitem.delete()
        return HttpResponse(status=200)

def shopitemdetail_list(request, item_id):
    if request.method != 'GET' and request.method != 'POST':
        return HttpResponseNotAllowed(['GET', 'POST'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if not ShopItem.objects.filter(id=item_id).exists():
        return HttpResponse(status=404)

    shopitem = ShopItem.objects.filter(id=item_id)
    
    detail_list= ShopItemDetail.objects.filter(shopitem=shopitem)

    if request.method == 'GET':
        if detail_list.count() <= 0:
            return JsonResponse([{}], safe=False, status=204)

        detail_all_list = [{ 'id' : detail.id, 'mainitem' : detail.main_item.id, 'color' : detail.color, 'size': detail.size, 'left_amount' : detail.left_amount } 
        for detail in detail_list]
    
        return JsonResponse(detail_all_list, safe=False, status=200)
    else:
        body = request.body.decode()
        detail_color = json.loads(body)['color']
        detail_size = json.loads(body)['size']
        detail_left_amount = json.loads(body)['left_amount']

        detail = ShopItemDetail(main_item=shopitem, color=detail_color, size=detail_size, left_amount=detail_left_amount)

        detail.save()
        
        response_dict = {'id' : detail.id, 'mainitem' : detail.main_item.id, 'color' : detail.color, 'size': detail.size, 'left_amount' : detail.left_amount }
        return JsonResponse(response_dict, status=201)
    

def shopitemdetail(request, detail_id):
    if request.method != 'GET' and request.method != 'PUT' and request.method != 'DELETE':
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if not ShopItemDetail.objects.filter(id=detail_id).exists():
        return HttpResponse(status=404)

    detail = ShopItemDetail.objects.get(id=detail_id)

    if detail.main_item.seller.id != request.user.id and (request.method == 'PUT' or request.method == 'DELETE'):
        return HttpResponse(status=403)

    if request.method == 'GET':
        response_dict = {'id' : detail.id, 'mainitem' : detail.main_item.id, 'color' : detail.color, 'size': detail.size, 'left_amount' : detail.left_amount }
        return JsonResponse(response_dict, status=200)
    elif request.method == 'PUT':
        body = request.body.decode()

        shopitemdetail_color = json.loads(body)['color']
        shopitemdetail_size = json.loads(body)['size']
        shopitemdetail_left_amount = json.loads(body)['left_amount']

        detail.color = shopitemdetail_color
        detail.size = shopitemdetail_size
        detail.left_amount = shopitemdetail_left_amount

        detail.save()

        response_dict = {'id' : detail.id, 'mainitem' : detail.main_item.id, 'color' : detail.color, 'size': detail.size, 'left_amount' : detail.left_amount }
        return JsonResponse(response_dict, status=200)
    else:
        detail.delete()
        return HttpResponse(status=200)

def reviewlist(request):
    if request.method != 'GET' and request.method != 'POST':
        return HttpResponseNotAllowed(['GET', 'POST'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if request.method == 'GET':
        if Review.objects.count() <= 0:
            return JsonResponse([{}], safe=False, status=204)

        review_all_list = [{ 'title' : review.title, 'content' : review.content, 'author': review.author.id } for review in Review.objects.all()]
        return JsonResponse(review_all_list, safe=False, status=200)
    else:
        body = request.body.decode()
        review_title = json.loads(body)['title']
        review_content = json.loads(body)['content']
        review_author = request.user

        review = Review(title=review_title, content=review_content, author=review_author)

        review.save()
        
        response_dict = {'id': review.id, 'title': review.title, 'content': review.content, 'author': review.author.id }
        return JsonResponse(response_dict, status=201)

def review(request, review_id):
    if request.method != 'GET' and request.method != 'PUT' and request.method != 'DELETE':
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if not Review.objects.filter(id=review_id).exists():
        return HttpResponse(status=404)

    review = Review.objects.get(id=review_id)

    if review.author.id != request.user.id and (request.method == 'PUT' or request.method == 'DELETE'):
        return HttpResponse(status=403)

    if request.method == 'GET':
        response_dict = { 'title': review.title, 'content': review.content, 'author': review.author.id }
        return JsonResponse(response_dict, status=200)
    elif request.method == 'PUT':
        body = request.body.decode()
        review_title = json.loads(body)['title']
        review_content = json.loads(body)['content']


        review.title = review_title
        review.content = review_content

        review.save()

        response_dict = {"id": review_id, "title": review.title, "content": review.content, "author" : review.author.id }
        return JsonResponse(response_dict, status=200)
    else:
        review.delete()
        return HttpResponse(status=200)

def reviewcomment(request, review_id):
    if request.method != 'GET' and request.method != 'POST':
        return HttpResponseNotAllowed(['GET', 'POST'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if not Review.objects.filter(id=review_id).exists():
        return HttpResponse(status=404)

    review = Review.objects.get(id=review_id)

    if request.method == 'GET':
        comment_list = Comment.objects.filter(review=review)

        if comment_list.count() <= 0:
            return JsonResponse([{}], safe=False, status=204)

        comment_json_list = [{ 'review' : comment.review.id, 'content' : comment.content, 'author': comment.author.id } for comment in comment_list]
        return JsonResponse(comment_json_list, safe=False, status=200)
    else:
        body = request.body.decode()
        comment_content = json.loads(body)['content']
        comment_author = request.user

        comment = Comment(review=review, content=comment_content, author=comment_author)

        comment.save()
        
        response_dict = {'id': comment.id, 'review': comment.review.id, 'content': comment.content, 'author': comment_author.id }
        return JsonResponse(response_dict, status=201)

def comment(request, comment_id):
    if request.method != 'GET' and request.method != 'PUT' and request.method != 'DELETE':
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if not Comment.objects.filter(id=comment_id).exists():
        return HttpResponse(status=404)

    comment = Comment.objects.get(id=comment_id)

    if comment.author.id != request.user.id and (request.method == 'PUT' or request.method == 'DELETE'):
        return HttpResponse(status=403)

    if request.method == 'GET':
        response_dict = { 'review': comment.review.id, 'content': comment.content, 'author': comment.author.id }
        return JsonResponse(response_dict, status=200)
    elif request.method == 'PUT':
        body = request.body.decode()
        comment_content = json.loads(body)['content']

        comment.content = comment_content

        comment.save()

        response_dict = {"id": comment_id, "review": comment.review.id, "content": comment.content, "author" : comment.author.id }
        return JsonResponse(response_dict, status=200)
    else:
        comment.delete()
        return HttpResponse(status=200)

