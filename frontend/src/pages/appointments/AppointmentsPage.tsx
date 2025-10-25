import React from 'react';
import { Box, Container, Typography } from '@mui/material';
import Navbar from '../../components/common/Navbar';
import Sidebar from '../../components/common/Sidebar';

const AppointmentsPage: React.FC = () => {
  return (
    <Box sx={{ display: 'flex' }}>
      <Navbar />
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" gutterBottom>
            Appointments
          </Typography>
          <Typography color="textSecondary">
            Appointments management coming soon...
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default AppointmentsPage;
