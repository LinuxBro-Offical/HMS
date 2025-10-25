import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  Grid,
  Chip,
} from '@mui/material';
import { ArrowBack, Edit } from '@mui/icons-material';
import Navbar from '../../components/common/Navbar';
import Sidebar from '../../components/common/Sidebar';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { fetchPatientById } from '../../store/slices/patientsSlice';
import { format } from 'date-fns';

const PatientDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { currentPatient } = useAppSelector((state) => state.patients);

  useEffect(() => {
    if (id) {
      dispatch(fetchPatientById(id));
    }
  }, [dispatch, id]);

  if (!currentPatient) {
    return (
      <Box sx={{ display: 'flex' }}>
        <Navbar />
        <Sidebar />
        <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
          <Container maxWidth="lg">
            <Typography>Loading...</Typography>
          </Container>
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <Navbar />
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Container maxWidth="lg">
          <Box sx={{ mb: 3 }}>
            <Button startIcon={<ArrowBack />} onClick={() => navigate('/patients')}>
              Back to Patients
            </Button>
          </Box>

          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h4">
              {currentPatient.first_name} {currentPatient.last_name}
            </Typography>
            <Button variant="contained" startIcon={<Edit />}>
              Edit Patient
            </Button>
          </Box>

          <Paper sx={{ p: 3 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Patient Code
                </Typography>
                <Typography variant="body1" gutterBottom>
                  {currentPatient.patient_code}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Status
                </Typography>
                <Chip
                  label={currentPatient.is_active ? 'Active' : 'Inactive'}
                  color={currentPatient.is_active ? 'success' : 'default'}
                  size="small"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Date of Birth
                </Typography>
                <Typography variant="body1">
                  {format(new Date(currentPatient.date_of_birth), 'MMMM dd, yyyy')}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Gender
                </Typography>
                <Typography variant="body1">{currentPatient.gender}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Phone
                </Typography>
                <Typography variant="body1">{currentPatient.phone}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Email
                </Typography>
                <Typography variant="body1">{currentPatient.email || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle2" color="textSecondary">
                  Address
                </Typography>
                <Typography variant="body1">
                  {currentPatient.address || 'N/A'}
                  {currentPatient.city && `, ${currentPatient.city}`}
                  {currentPatient.state && `, ${currentPatient.state}`}
                  {currentPatient.postal_code && ` ${currentPatient.postal_code}`}
                </Typography>
              </Grid>
              {currentPatient.blood_group && (
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Blood Group
                  </Typography>
                  <Typography variant="body1">{currentPatient.blood_group}</Typography>
                </Grid>
              )}
            </Grid>
          </Paper>
        </Container>
      </Box>
    </Box>
  );
};

export default PatientDetailsPage;
