import React, { useState } from "react";
import AuthSkeleton from "./AuthSkeleton";
import { registerRequest } from "./authSlice";
import { useDispatch, useSelector } from "react-redux";

const Register = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const dispatch = useDispatch();
    const { loading, error } = useSelector((state) => state.auth);

    const handleRegister = async (e) => {
        e.preventDefault();
        dispatch(registerRequest({username, password}))
    };

    const fields = [
        { label: "Username", type: "text", value: username, onChange: (e) => setUsername(e.target.value) },
        { label: "Password", type: "password", value: password, onChange: (e) => setPassword(e.target.value) },
    ];

    return <AuthSkeleton title="Register" fields={fields} buttonText="Register" onSubmit={handleRegister} />;
};

export default Register;
