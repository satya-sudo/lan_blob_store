import { createGlobalStyle } from "styled-components";

export const GlobalStyles = createGlobalStyle`
    body {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }

    input, button {
        background-color: #1f1f1f;
        color: #ffffff;
        border: 1px solid #00bcd4; /* Cyan as the secondary color */
        padding: 10px;
        border-radius: 5px;
    }

    button {
        cursor: pointer;
        &:hover {
            background-color: #00bcd4; /* Cyan on hover */
            color: #121212;
        }
    }

    a {
        color: #00bcd4;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
`;
