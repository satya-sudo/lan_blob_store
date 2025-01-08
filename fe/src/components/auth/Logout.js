// src/components/Logout.js
import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "./authSlice";
import { useNavigate } from "react-router-dom";
import {
    ListItem,
    ListItemIcon,
    ListItemText,
    Tooltip,
  } from "@mui/material";
import {
    Logout,
} from "@mui/icons-material";

const LogoutSection = ({collapsed}) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { user } = useSelector((state) => state.auth);

    useEffect(() => {
        if (!user) {
            navigate("/login");
        }
    }, [user, navigate]);

    const handleLogout = (e) => {
        e.preventDefault();
        dispatch(logout());
    };
    return (
        <div>
          <Tooltip title={collapsed ? "Logout" : ""} placement="left">
            <ListItem button onClick={handleLogout}>
              <ListItemIcon style={{ color: "#00bcd4" }}>
                <Logout />
              </ListItemIcon>
              {!collapsed && <ListItemText primary="Logout" />}
            </ListItem>
          </Tooltip>
        </div>
    );
};

export default LogoutSection;
