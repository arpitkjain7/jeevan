import React from 'react';
import { Box, Typography, Grid } from '@mui/material';

const RegisterationConfirmation = () => {
  const data = [
    { key: 'Key 1', value: 'Value 1' },
    { key: 'Key 2', value: 'Value 2' },
    { key: 'Key 3', value: 'Value 3' },
    { key: 'Key 4', value: 'Value 4' },
    { key: 'Key 5', value: 'Value 5' },
    { key: 'Key 6', value: 'Value 6' },
  ];

  return (
    <Box padding={2}>
      <Typography variant="h6" color="primary" gutterBottom>
        Success
      </Typography>
      <Grid container spacing={2} xs={10}>
        {data.map((item) => (
          <Grid item key={item.key} xs={2}>
            <Typography variant="subtitle1" gutterBottom>
              {item.key}
            </Typography>
            <Typography variant="body1" gutterBottom>
              {item.value}
            </Typography>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default RegisterationConfirmation;
