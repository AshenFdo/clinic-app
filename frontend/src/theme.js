import {createTheme} from '@mui/material/styles';


const fontSizes = {
  xs: "0.75rem",
  sm: "0.875rem",
  base: "1rem",
  md: "1.125rem",
  lg: "1.25rem",
  xl: "1.5rem",
  "2xl": "2rem",
  "3xl": "2.5rem",
  "4xl": "3rem",
};

const theme = createTheme({
  palette: {
    primary: {
      main: "#2B6CB0",      
      light: "#2E5BA8",
      dark: "#142952",
    },
    secondary: {
      main: "#2e8653",     
    },
    Tertiary:{
      main: "#A0AEC0"
      
    },
    background: {
      default: "#F8F9FA",
      paper: "#FFFFFF",
    },
    text:{
      primary: "#1A202C",
      secondary: "#4A5568",
    },

  },
  typography: {
    fontFamily: "'Manrope', sans-serif",
    fontSize: 16,
    body1: {
      fontFamily: "'Inter', sans-serif",
      fontSize: fontSizes.base,
      fontWeight: 400,
      lineHeight: 1.6,
    },
    body2: {
      fontFamily: "'Inter', sans-serif",
      fontSize: fontSizes.sm,
      fontWeight: 400,
      lineHeight: 1.5,
    },
    h1: { fontWeight: 800, fontSize: fontSizes["4xl"], lineHeight: 1.1 },
    h2: { fontWeight: 700, fontSize: fontSizes["3xl"], lineHeight: 1.15 },
    h3: { fontWeight: 700, fontSize: fontSizes["2xl"], lineHeight: 1.2 },
    h4: { fontWeight: 700, fontSize: fontSizes.xl, lineHeight: 1.25 },
    h5: { fontWeight: 600, fontSize: fontSizes.lg, lineHeight: 1.3 },
    h6: { fontWeight: 600, fontSize: fontSizes.md, lineHeight: 1.35 },
    button: { fontSize: fontSizes.sm, fontWeight: 600 },
    caption: { fontSize: fontSizes.xs },



  },
  shape: {
    borderRadius: 10,      
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",             
          fontWeight: 600,
          borderRadius: "8px",
        },
        containedPrimary: {
          height: 52,
          borderRadius: "12px",
          background: "linear-gradient(135deg, #005394 0%, #003a6b 100%)",
          fontFamily: "'Manrope', sans-serif",
          fontWeight: 700,
          fontSize: "0.95rem",
          letterSpacing: "0.01em",
          textTransform: "none",
          boxShadow: "0 4px 20px rgba(0,83,148,0.25)",
          transition: "all 0.2s ease",
          "&:hover": {
            background: "linear-gradient(135deg, #004280 0%, #002855 100%)",
            boxShadow: "0 6px 28px rgba(0,83,148,0.35)",
            transform: "translateY(-1px)",
          },
          "&.Mui-disabled": {
            background: "#e5e7eb",
            boxShadow: "none",
            transform: "none",
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
          borderRadius: "12px",
        },
      },
    },
  },
  
});

export default theme;
