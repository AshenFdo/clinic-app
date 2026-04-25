import React, { useEffect, useState } from 'react'
import { useAuth } from '../../hooks/useAuth.js';
import { Box, Typography, CircularProgress, Alert } from '@mui/material';


const UserSample = () => {
    const { getUserData } = useAuth();
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
      const loadUser = async () => {
        try {
          const data = await getUserData();
          setUserData(data);
        } catch (err) {
          setError(err.response?.data?.detail || 'Failed to load user data.');
        } finally {
          setLoading(false);
        }
      };

      loadUser();
    }, []);

    if (loading) {
      return (
        <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <CircularProgress />
        </Box>
      );
    }

    if (error) {
      return (
        <Box sx={{ p: 4 }}>
          <Alert severity='error'>{error}</Alert>
        </Box>
      );
    }

  return (
    <Box sx={{ p: 4, display: 'grid', gap: 1 }}>
      <Typography variant='h4'>Welcome</Typography>
      <Typography><strong>Name:</strong> {userData?.full_name}</Typography>
      <Typography><strong>Email:</strong> {userData?.email}</Typography>
      <Typography><strong>Role:</strong> {userData?.role}</Typography>
      <Typography><strong>Mobile:</strong> {userData?.mobile_no}</Typography>
      <Typography><strong>Gender:</strong> {userData?.gender}</Typography>
      <Typography><strong>Date of Birth:</strong> {userData?.date_of_birth}</Typography>
    </Box>
  )
}

export default UserSample