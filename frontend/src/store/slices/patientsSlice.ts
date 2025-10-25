import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { patientsAPI } from '../../api/patients.api';
import { Patient, PatientFormData } from '../../types/patient.types';
import { LoadingState } from '../../types/common.types';

interface PatientsState {
  patients: Patient[];
  currentPatient: Patient | null;
  total: number;
  loading: LoadingState;
  error: string | null;
}

const initialState: PatientsState = {
  patients: [],
  currentPatient: null,
  total: 0,
  loading: 'idle',
  error: null,
};

export const fetchPatients = createAsyncThunk(
  'patients/fetchAll',
  async (params: { page?: number; search?: string } | undefined = undefined, { rejectWithValue }) => {
    try {
      return await patientsAPI.getAll(params);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch patients');
    }
  }
);

export const fetchPatientById = createAsyncThunk(
  'patients/fetchById',
  async (id: string, { rejectWithValue }) => {
    try {
      return await patientsAPI.getById(id);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch patient');
    }
  }
);

export const createPatient = createAsyncThunk(
  'patients/create',
  async (data: PatientFormData, { rejectWithValue }) => {
    try {
      return await patientsAPI.create(data);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create patient');
    }
  }
);

export const updatePatient = createAsyncThunk(
  'patients/update',
  async ({ id, data }: { id: string; data: Partial<PatientFormData> }, { rejectWithValue }) => {
    try {
      return await patientsAPI.update(id, data);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update patient');
    }
  }
);

export const deletePatient = createAsyncThunk(
  'patients/delete',
  async (id: string, { rejectWithValue }) => {
    try {
      await patientsAPI.delete(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to delete patient');
    }
  }
);

const patientsSlice = createSlice({
  name: 'patients',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentPatient: (state) => {
      state.currentPatient = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchPatients.pending, (state) => {
        state.loading = 'pending';
      })
      .addCase(fetchPatients.fulfilled, (state, action) => {
        state.loading = 'succeeded';
        state.patients = action.payload.results;
        state.total = action.payload.count;
      })
      .addCase(fetchPatients.rejected, (state, action) => {
        state.loading = 'failed';
        state.error = action.payload as string;
      })
      .addCase(fetchPatientById.fulfilled, (state, action) => {
        state.currentPatient = action.payload;
      })
      .addCase(createPatient.fulfilled, (state, action) => {
        state.patients.unshift(action.payload);
      })
      .addCase(updatePatient.fulfilled, (state, action) => {
        const index = state.patients.findIndex(p => p.id === action.payload.id);
        if (index !== -1) {
          state.patients[index] = action.payload;
        }
        if (state.currentPatient?.id === action.payload.id) {
          state.currentPatient = action.payload;
        }
      })
      .addCase(deletePatient.fulfilled, (state, action) => {
        state.patients = state.patients.filter(p => p.id !== action.payload);
      });
  },
});

export const { clearError, clearCurrentPatient } = patientsSlice.actions;
export default patientsSlice.reducer;
