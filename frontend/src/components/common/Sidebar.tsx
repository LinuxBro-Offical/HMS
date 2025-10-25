import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Divider,
} from '@mui/material';
import {
  Dashboard,
  People,
  CalendarMonth,
  Assignment,
  Receipt,
  Biotech,
  Inventory,
  BarChart,
} from '@mui/icons-material';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <Dashboard />, path: '/dashboard' },
  { text: 'Patients', icon: <People />, path: '/patients' },
  { text: 'Appointments', icon: <CalendarMonth />, path: '/appointments' },
  { text: 'Encounters', icon: <Assignment />, path: '/encounters' },
  { text: 'Billing', icon: <Receipt />, path: '/billing' },
  { text: 'Laboratory', icon: <Biotech />, path: '/laboratory' },
  { text: 'Inventory', icon: <Inventory />, path: '/inventory' },
  { text: 'Analytics', icon: <BarChart />, path: '/analytics' },
];

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      <Toolbar />
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => navigate(item.path)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;
