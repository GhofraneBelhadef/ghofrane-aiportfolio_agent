import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale);

const DashboardAnalytics = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/analytics').then((res) => setData(res.data));
  }, []);

  const chartData = {
    labels: data.map((item) => item.question),
    datasets: [
      {
        label: 'Nombre de demandes',
        data: data.map((item) => item.count),
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
      },
    ],
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Tendances d’utilisation</h2>
      <Bar data={chartData} />
    </div>
  );
};

export default DashboardAnalytics;