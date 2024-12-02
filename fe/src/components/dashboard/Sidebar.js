import React from "react";
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Tooltip,
} from "@mui/material";
import { Movie, Audiotrack, Description, Photo, Settings, Menu } from "@mui/icons-material";
import styled from "styled-components";

const SidebarContainer = styled.div`
  width: ${(props) => (props.collapsed ? "80px" : "250px")};
  background-color: #1f1f1f;
  height: 100%;
  transition: width 0.3s ease-in-out;
  display: flex;
  flex-direction: column;
`;

const SidebarHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: ${(props) => (props.collapsed ? "center" : "space-between")};
  padding: 20px;
  color: #00bcd4;
  border-bottom: 1px solid #00bcd4;
  transition: justify-content 0.3s ease-in-out;
`;

const menuItems = [
  { text: "Videos", icon: <Movie />, path: "/videos" },
  { text: "Audio", icon: <Audiotrack />, path: "/audio" },
  { text: "Docs", icon: <Description />, path: "/docs" },
  { text: "Photos", icon: <Photo />, path: "/photos" },
  { text: "Settings", icon: <Settings />, path: "/settings" },
];

const Sidebar = ({ collapsed }) => {
  return (
    <Drawer
      variant="permanent"
      PaperProps={{
        style: {
          width: collapsed ? "80px" : "250px",
          backgroundColor: "#1f1f1f",
          color: "#ffffff",
          top: '64px',
          padding:'20px'
        },
      }}
    >
      <SidebarContainer collapsed={collapsed}>
        <List sx={{"alignItems":"center"}}>
          {menuItems.map((item, index) => (
            <Tooltip
              key={index}
              title={collapsed ? item.text : ""}
              placement="left"
            >
              <ListItem button>
                <ListItemIcon style={{ color: "#00bcd4" }}>{item.icon}</ListItemIcon>
                {!collapsed && <ListItemText primary={item.text} />}
              </ListItem>
            </Tooltip>
          ))}
        </List>
      </SidebarContainer>
    </Drawer>
  );
};

export default Sidebar;
