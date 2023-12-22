import React, { useState } from 'react';
import { TextField, Button, Container, Typography } from '@material-ui/core';

function RequestForm() {
  const [request, setRequest] = useState({
    fieldName: '',
    workDetails: ''
  });

  const handleChange = (e) => {
    setRequest({ ...request, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // כאן אפשר לשלוח את הנתונים לשרת
    console.log(request);
  };

  return (
    <Container>
      <Typography variant="h4">הגשת דרישה לעזרה בחקלאות</Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="שם השדה"
          name="fieldName"
          value={request.fieldName}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="פרוט העבודה הנדרשת"
          name="workDetails"
          value={request.workDetails}
          onChange={handleChange}
          fullWidth
          margin="normal"
          multiline
          rows={4}
        />
        <Button type="submit" color="primary" variant="contained">שלח</Button>
      </form>
    </Container>
  );
}

export default RequestForm;
