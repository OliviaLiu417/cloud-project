"use client";
import React, { useState, useEffect, forwardRef } from "react";
import { Doughnut } from "react-chartjs-2";
import "chart.js/auto";

const colors = [
  "#FF6384",
  "#36A2EB",
  "#FFCE56",
  "#4BC0C0",
  "#9966FF",
  "#FF9F40",
  "#E7E9ED",
];

const SourceChart = forwardRef(
  ({ category, setSelectedSource, counts }, ref) => {
    const [renderData, setRenderData] = useState();
    useEffect(() => {
      const entries = Object.entries(counts);
      entries.sort((a, b) => b[1] - a[1]);
      const sortedEntries = entries.slice(0, 7);
      const sortedData = Object.fromEntries(sortedEntries);
      const data = {
        labels: Object.keys(sortedData),
        datasets: [
          {
            label: "Sources",
            data: Object.values(sortedData),
            backgroundColor: colors,
            borderWidth: 1,
          },
        ],
      };
      setRenderData(data);
    }, [category, counts]);

    const handleClick = (_event, elements) => {
      if (elements.length !== 0) {
        const elementIndex = elements[0].index;
        const label = renderData.labels[elementIndex];
        setSelectedSource(label);
      }
    };

    const options = {
      maintainAspectRatio: false,
      onClick: handleClick,
    };

    return (
      <div style={{ width: "300px", height: "300px" }} ref={ref}>
        {renderData && <Doughnut data={renderData} options={options} />}
      </div>
    );
  }
);

SourceChart.displayName = "SourceChart";

export default SourceChart;
