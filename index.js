import http from 'k6/http';
import { check, group } from 'k6';
import { Trend } from 'k6/metrics'; // For custom metrics

const BASE_URL = 'http://localhost:8080/v1'; // Replace with your server's base URL

// Define custom metrics to record the execution time of each group
let openAlarmDuration = new Trend('open_alarm_duration');
let closeAlarmDuration = new Trend('close_alarm_duration');
let suspendAlarmDuration = new Trend('suspend_alarm_duration');
let processAlarmDuration = new Trend('process_alarm_duration');

export let options = {
  vus: 1,       
  iterations: 30, // Total iterations will be the number of groups times the number of repetitions per group
};

export default function () {
  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzE5MDQyMzUsImlzcyI6ImFsYXJtLXN5c3RlbSIsInVzZXJuYW1lIjoicXkifQ.jn1BrqOA47O_uCZPHR3_QmbaJrwVSdLCOVzurPUZO5M', 
  };

  let startTime = Date.now();
  group('getOpenAlarms', () => {
    let res = http.post(`${BASE_URL}/getOpenAlarms`, JSON.stringify({}), { headers });

    check(res, {
      'Ping: status is 200': (r) => r.status === 200,
    });
  });
  openAlarmDuration.add(Date.now() - startTime);


// Group 2: Get Close Alarms
  startTime = Date.now();
  group('getCloseAlarms', () => {
    let res = http.post(`${BASE_URL}/getCloseAlarms`, JSON.stringify({}), { headers });

    check(res, {
      'Ping: status is 200': (r) => r.status === 200,
    });
  });
  closeAlarmDuration.add(Date.now() - startTime);



  startTime = Date.now();
  group('getSuspendAlarms', () => {
    let res = http.post(`${BASE_URL}/getSuspendAlarms`, JSON.stringify({}), { headers });

    check(res, {
      'Ping: status is 200': (r) => r.status === 200,
    });
  });
  suspendAlarmDuration.add(Date.now() - startTime);



  startTime = Date.now();
  group('getProcessAlarms', () => {
    let res = http.post(`${BASE_URL}/getProcessAlarms`, JSON.stringify({}), { headers });

    check(res, {
      'Healthy: status is 200': (r) => r.status === 200,
    });
  });
  processAlarmDuration.add(Date.now() - startTime);

}
