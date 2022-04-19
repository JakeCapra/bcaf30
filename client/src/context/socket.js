import { io } from 'socket.io-client';

import React from 'react';

const serverEndpoint = "http://localhost:8000";

export const socket = io(serverEndpoint);
socket.on('connect', () => {
  console.log('connected to server');
});
export const SocketContext = React.createContext();
