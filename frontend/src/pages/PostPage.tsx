import React from 'react'
import { Col, Container, Row } from 'react-bootstrap'
import { useDispatch } from 'react-redux'
import Post from '../components/Post'
import PostComments from '../components/PostComments'
import TopBar from '../components/TopBar'
import { AppDispatch } from '../store'
import Footer from '../components/Footer'
/*eslint-disable */

export default function PostPage (): JSX.Element {
  const dispatch = useDispatch<AppDispatch>()
  return (<div>
    <TopBar />
    <Container>
      <Row>
        <Col>
          <Post />
        </Col>
        <Col>
          <PostComments review_id={1} />
        </Col>
      </Row>
    </Container>
    <Footer/>
  </div>)
}
