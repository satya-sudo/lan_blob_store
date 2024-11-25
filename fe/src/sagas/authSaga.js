import { call, put, takeLatest } from "redux-saga/effects";
import axios from "../utils/axios"
import {
    loginRequest,
    loginSuccess,
    loginFailure,
    registerRequest,
    registerSuccess,
    registerFailure,
} from "../components/auth/authSlice";
import { showSuccessToast, showErrorToast } from "../utils/toast";

function* handleLogin(action) {
    try {
        const response = yield call(axios.post, "/auth/login", {
            username: action.payload.username,
            password: action.payload.password,
        });
        yield put(loginSuccess(response.data));
        showSuccessToast("Login successful!");
    } catch (error) {
        yield put(loginFailure(error.response?.data || error.message));
        showErrorToast(error.response?.data?.message || "Login failed!");
    }
}

function* handleRegister(action) {
    try {
        const response = yield call(axios.post, "/auth/register", {
            username: action.payload.username,
            password: action.payload.password,
        });
        yield put(registerSuccess(response.data));
        showSuccessToast("Registration successful!");
    } catch (error) {
        yield put(registerFailure(error.response?.data || error.message));
        showErrorToast(error.response?.data?.message || "Registration failed!");
    }
}

export function* authSaga() {
    yield takeLatest(loginRequest.type, handleLogin);
    yield takeLatest(registerRequest.type, handleRegister);
}
