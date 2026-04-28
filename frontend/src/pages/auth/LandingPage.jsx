import React from 'react'

import {
    Typography,
    Box,

} from '@mui/material'
import NavigationBar from '../../components/ui/NavigationBar';
import Fade from '@mui/material/Fade';


const LandingPage = () => {
    const [mounted, setMounted] = React.useState(false);

    React.useEffect(() => {
        setMounted(true);
    }, []);

    return (
        <>
            <NavigationBar />

            <Fade in={mounted} timeout={900} appear>
                <Box sx={{ textAlign: 'center', mt: 6, px: 2 }}>
                    <Typography variant="h2" sx={{ fontWeight: 700 }}>
                        Welcome to Our Clinic!
                    </Typography>
                    <Typography variant="h5" sx={{ mt: 2 }}>
                        Your health, our priority. Book your appointment today!
                    </Typography>
                </Box>
            </Fade>

        </>
    )
}

export default LandingPage