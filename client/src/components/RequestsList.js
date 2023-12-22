import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Container } from '@material-ui/core';

function RequestsList() {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    // כאן ניתן לטעון נתונים מהשרת
    setRequests([{ fieldName: 'שדה דוגמה', workDetails: 'פרטי עבודה' }]);
  }, []);

  return (
    <Container>
      {requests.map((request, index) => (
        <Card key={index}>
          <CardContent>
            <Typography variant="h5">{request.fieldName}</Typography>
            <Typography>{request.workDetails}</Typography>
          </CardContent>
        </Card>
      ))}
    </Container>
  );
}

export default RequestsList;
