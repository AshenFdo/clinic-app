import React from 'react'
import { NavLink } from 'react-router-dom'
import { AppBar, Box, Button, Toolbar, Typography } from '@mui/material'

const menuItems = [
    { label: 'Home', to: '/landing' },
    { label: 'About', to: '/about' },
    { label: 'Doctor', to: '/doctors' },
    { label: 'Contact', to: '/contact' },
]

const NavigationBar = () => {

    return (
        <AppBar
            position="static"
            elevation={0}
            sx={{
                bgcolor: '#f7fafc',
                color: 'text.primary',
                borderBottom: '1px solid',
                borderColor: 'divider',
                backdropFilter: 'blur(10px)',
            }}
        >
            <Toolbar
                sx={{
                    minHeight: { xs: 72, md: 84 },
                    px: { xs: 2, sm: 3, md: 4 },
                    gap: 2,
                }}
            >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, minWidth: 'fit-content' }}>
                    <Box
                        sx={{
                            width: 40,
                            height: 40,
                            borderRadius: '50%',
                            display: 'grid',
                            placeItems: 'center',
                            bgcolor: 'primary.main',
                            color: 'primary.contrastText',
                            fontWeight: 700,
                            boxShadow: '0 8px 20px rgba(63, 81, 181, 0.25)',
                        }}
                    >
                        S
                    </Box>
                    <Typography variant="h6" sx={{ fontWeight: 700, letterSpacing: 0.2 }}>
                        Suhada Clinic
                    </Typography>
                </Box>

                <Box
                    sx={{
                        flex: 1,
                        display: { xs: 'none', md: 'flex' },
                        justifyContent: 'center',
                        gap: 1,
                    }}
                >
                    {menuItems.map((item) => (
                        <Button
                            key={item.label}
                            component={NavLink}
                            to={item.to}
                            end={item.to === '/landing'}
                            variant="text"
                            sx={{
                                color: 'text.primary',
                                fontWeight: 600,
                                px: 2,
                                borderRadius: 999,
                                textTransform: 'none',
                                '&:hover': { bgcolor: 'action.hover' },
                                '&.active': {
                                    bgcolor: 'primary.main',
                                    color: 'primary.contrastText',
                                    '&:hover': { bgcolor: 'primary.dark' },
                                },
                            }}
                        >
                            {item.label}
                        </Button>
                    ))}
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, ml: 'auto' }}>
                    <Button
                        variant="outlined"
                        component={NavLink}
                        to="/login"
                        sx={{
                            textTransform: 'none',
                            fontWeight: 600,
                            borderRadius: 999,
                            px: { xs: 2, sm: 3 },
                            '&.active': {
                                bgcolor: 'primary.main',
                                color: 'primary.contrastText',
                                borderColor: 'primary.main',
                            },
                        }}
                    >
                        Login
                    </Button>
                    <Button
                        variant="contained"
                        component={NavLink}
                        to="/register"
                        sx={{
                            textTransform: 'none',
                            fontWeight: 700,
                            borderRadius: 999,
                            px: { xs: 2, sm: 3 },
                            boxShadow: 'none',
                            '&.active': {
                                bgcolor: 'primary.dark',
                            },
                        }}
                    >
                        Sign In
                    </Button>
                </Box>
            </Toolbar>
        </AppBar>
    )
}

export default NavigationBar