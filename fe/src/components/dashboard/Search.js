import React, { useState } from "react";
import { TextField, IconButton } from "@mui/material";
import { Search as SearchIcon } from "@mui/icons-material";
import styled from "styled-components";

const SearchWrapper = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 64px;
`;

const SearchInput = styled(TextField)`
  background-color: #1f1f1f;
  color: #ffffff;
  width: 70wh; 
  border-radius: 40px; 
  input {
    color: white;
  }

  .MuiOutlinedInput-root {
    border-radius: 50px; 
    padding: 10px;
  }

  .MuiInputAdornment-root {
    margin-right: 5px; 
  }
`;

const Search = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    onSearch(query);
  };

  return (
    <SearchWrapper>
      <SearchInput
        variant="outlined"
        placeholder="Search Media..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        InputProps={{
          endAdornment: (
            <IconButton onClick={handleSearch} color="inherit">
              <SearchIcon />
            </IconButton>
          ),
        }}
      />
    </SearchWrapper>
  );
};

export default Search;
