import React from "react";
import { Box, Typography, TextField, Button } from "@mui/material";
import StorageIcon from "@mui/icons-material/Storage";

const FormSkeleton = ({ title, fields, buttonText, onSubmit }) => (
    <Box
        sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            height: "100vh",
            backgroundColor: "#121212",
            color: "#ffffff",
        }}
    >
        <StorageIcon sx={{ fontSize: 80, color: "#00bcd4", mb: 2 }} />

        <Typography variant="h4" gutterBottom>
            {title}
        </Typography>

        <Box
            component="form"
            onSubmit={onSubmit}
            sx={{
                display: "flex",
                flexDirection: "column",
                gap: 2,
                width: "100%",
                maxWidth: 400,
            }}
        >
            {fields.map((field, index) => (
                <TextField
                    key={index}
                    label={field.label}
                    type={field.type}
                    variant="outlined"
                    fullWidth
                    value={field.value}
                    onChange={field.onChange}
                    InputProps={{ style: { color: "#ffffff" } }}
                    InputLabelProps={{ style: { color: "#ffffff" } }}
                    sx={{
                        "& .MuiOutlinedInput-root": {
                            "& fieldset": { borderColor: "#00bcd4" },
                            "&:hover fieldset": { borderColor: "#00bcd4" },
                        },
                    }}
                />
            ))}
            <Button
                type="submit"
                variant="contained"
                sx={{
                    backgroundColor: "#00bcd4",
                    "&:hover": { backgroundColor: "#008c9e" },
                }}
            >
                {buttonText}
            </Button>
        </Box>
    </Box>
);

export default FormSkeleton;
