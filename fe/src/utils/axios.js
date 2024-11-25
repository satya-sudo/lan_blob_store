import axios from "axios";

const axiosInstance = axios.create({
    baseURL: "http://Satyams-MacBook-Pro.local:5872", // Default base URL
    timeout: 10000, // Request timeout in milliseconds
    headers: {
        "Content-Type": "application/json",
    },
});

axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("authToken");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        // Handle errors globally
        if (error.response?.status === 401) {
            // Example: Automatically logout on 401
            console.error("Unauthorized. Logging out...");
            localStorage.removeItem("authToken");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;
