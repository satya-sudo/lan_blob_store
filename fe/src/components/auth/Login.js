// src/components/Login.js
import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { loginRequest } from "./authSlice";
import AuthSkeleton from "./AuthSkeleton";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { user, loading, error } = useSelector((state) => state.auth);

    useEffect(() => {
        if (user) {
            navigate("/dashboard");
        }
    }, [user, navigate]);

    const handleSubmit = (e) => {
        e.preventDefault();
        dispatch(loginRequest({ username, password }));
    };

    const fields = [
        { label: "Username", type: "text", value: username, onChange: (e) => setUsername(e.target.value) },
        { label: "Password", type: "password", value: password, onChange: (e) => setPassword(e.target.value) },
    ];

    return (
        <AuthSkeleton
            title="Login"
            fields={fields}
            buttonText={loading ? "Logging in..." : "Login"}
            onSubmit={handleSubmit}
            error={error && error.message}
        />
    );
};

export default Login;
