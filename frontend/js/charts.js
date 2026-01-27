let distributionChartInstance = null;
let groupChartInstance = null;
let subjectChartInstance = null;

function renderDistributionChart(scores) {
  const buckets = Array.from({ length: 10 }, (_, index) => ({
    label: `${index * 10}-${index * 10 + 9}`,
    count: 0,
  }));

  scores.forEach((score) => {
    const index = Math.min(Math.floor(score / 10), 9);
    buckets[index].count += 1;
  });

  if (distributionChartInstance) distributionChartInstance.destroy();
  const ctx = document.getElementById("distributionChart");
  distributionChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: buckets.map((b) => b.label),
      datasets: [
        {
          label: "Количество оценок",
          data: buckets.map((b) => b.count),
          backgroundColor: "#4c7cf0",
        },
      ],
    },
  });
}

function renderGroupChart(groupCounts) {
  if (groupChartInstance) groupChartInstance.destroy();
  const ctx = document.getElementById("groupChart");
  groupChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels: Object.keys(groupCounts),
      datasets: [
        {
          data: Object.values(groupCounts),
          backgroundColor: ["#4c7cf0", "#7dd3fc", "#f59e0b", "#22c55e"],
        },
      ],
    },
  });
}

function renderSubjectChart(subjectAverages) {
  if (subjectChartInstance) subjectChartInstance.destroy();
  const ctx = document.getElementById("subjectChart");
  subjectChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: Object.keys(subjectAverages),
      datasets: [
        {
          label: "Средний балл",
          data: Object.values(subjectAverages),
          borderColor: "#ef4444",
          tension: 0.3,
        },
      ],
    },
  });
}

window.renderDistributionChart = renderDistributionChart;
window.renderGroupChart = renderGroupChart;
window.renderSubjectChart = renderSubjectChart;
