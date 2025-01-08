import React, { useState } from "react";
import { AppBar, Toolbar, Typography, Box, Grid, Tooltip, IconButton } from "@mui/material";
import Sidebar from "./Sidebar";
import Search from "./Search";
import styled from "styled-components";
import { Menu } from "@mui/icons-material";

const MainContent = styled.div`
  margin-left: ${(props) => (props.collapsed ? "80px" : "250px")};
  padding: 20px;
  background-color: #121212;
  min-height: 100vh;
  color: #ffffff;
  transition: margin-left 0.3s ease-in-out;
`;

const DashboardAppBar = styled(AppBar)`
  background-color: #1f1f1f !important;
`;

const SearchWrapper = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 20px;
`;

const Dashboard = () => {
  const [collapsed, setCollapsed] = useState(false);

  const handleToggleSidebar = () => {
    setCollapsed(!collapsed);
  };
  const handleSearch = (query) => {
    console.log("Search query:", query); 
  };

  return (
    <Box>
      <DashboardAppBar position="fixed">
        <Toolbar>
        <Tooltip title={collapsed ? "Expand" : "Collapse"} placement="right">
            <IconButton onClick={handleToggleSidebar} color="inherit">
              <Menu />
            </IconButton>
          </Tooltip>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Dashboard
          </Typography>
        </Toolbar>
      </DashboardAppBar>

      <Sidebar collapsed={collapsed} />

      <SearchWrapper>
        <Search onSearch={handleSearch} />
      </SearchWrapper>

      <MainContent collapsed={collapsed}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h4" gutterBottom>
              Welcome to the Dashboard
            </Typography>
            <Typography>
             some date place holder for now
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box
              style={{
                backgroundColor: "#1f1f1f",
                padding: "20px",
                borderRadius: "8px",
              }}
            >
              <Typography variant="h6" gutterBottom>
                Section 1
              </Typography>
              <Typography>Details for section 1...</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box
              style={{
                backgroundColor: "#1f1f1f",
                padding: "20px",
                borderRadius: "8px",
              }}
            >
              <Typography variant="h6" gutterBottom>
                Section 2
              </Typography>
              <Typography>Details for section 2...</Typography>
            </Box>
          </Grid>
        </Grid>
      </MainContent>
    </Box>
  );
};

export default Dashboard;
