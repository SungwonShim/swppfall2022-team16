import { createSlice } from '@reduxjs/toolkit'
import axios from 'axios'

/*eslint-disable */
/*eslint no-multiple-empty-lines: "error"*/

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export interface UserShopInfo {
    id: number
    credit: number
    cart: string
    favorite_clothes : string
    purchased_item : string
}

export interface UserState {
    usershop: UserShopInfo | null
}

const initialState : UserState = {
    usershop: null
}

export const userShopSlice = createSlice({
    name: "usershop",
    initialState,
    reducers:{},
    extraReducers: (builder) => {},
});

export const userShopActions = userShopSlice.actions;

export default userShopSlice.reducer;