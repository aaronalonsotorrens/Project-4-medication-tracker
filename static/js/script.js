document.addEventListener("DOMContentLoaded", function () {
  const medCtx = document.getElementById("medCategoryChart")?.getContext("2d");
  const sideEffectCtx = document
    .getElementById("sideEffectChart")
    ?.getContext("2d");
  const genderSelect = document.getElementById("genderSelect");

  if (!medCtx || !sideEffectCtx || !genderSelect) return;

  const genderMedicationData = window.genderMedicationData || {};
  const genderSideEffectData = window.genderSideEffectData || {};

  let medChart = null;
  let sideEffectChart = null;

  function renderCharts(gender) {
    const medData = genderMedicationData[gender] || genderMedicationData["All"];
    const seData = genderSideEffectData[gender] || genderSideEffectData["All"];

    // Destroy old charts if they exist
    if (medChart) medChart.destroy();
    if (sideEffectChart) sideEffectChart.destroy();

    // Medication Chart
    medChart = new Chart(medCtx, {
      type: "pie",
      data: {
        labels: medData.labels,
        datasets: [
          {
            label: `Medications - ${gender}`,
            data: medData.counts,
            backgroundColor: [
              "#007bff",
              "#6610f2",
              "#6f42c1",
              "#e83e8c",
              "#fd7e14",
              "#20c997",
            ],
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            position: "top",
          },
          datalabels: {
            formatter: (value, ctx) => {
              const sum = ctx.chart.data.datasets[0].data.reduce(
                (a, b) => a + b,
                0
              );
              return ((value * 100) / sum).toFixed(1) + "%";
            },
            color: "#fff",
            font: { weight: "bold" },
          },
        },
      },
      plugins: [ChartDataLabels],
    });

    // Side Effect Chart
    sideEffectChart = new Chart(sideEffectCtx, {
      type: "pie",
      data: {
        labels: seData.labels,
        datasets: [
          {
            label: `Side Effects - ${gender}`,
            data: seData.counts,
            backgroundColor: [
              "#dc3545",
              "#ffc107",
              "#28a745",
              "#17a2b8",
              "#6c757d",
              "#343a40",
            ],
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            position: "top",
          },
          datalabels: {
            formatter: (value, ctx) => {
              const sum = ctx.chart.data.datasets[0].data.reduce(
                (a, b) => a + b,
                0
              );
              return ((value * 100) / sum).toFixed(1) + "%";
            },
            color: "#fff",
            font: { weight: "bold" },
          },
        },
      },
      plugins: [ChartDataLabels],
    });
  }

  // Attach event listener for dropdown
  genderSelect.addEventListener("change", function () {
    renderCharts(this.value);
  });

  // Initial chart render
  const selectedGender = genderSelect.dataset.selectedGender || "All";
  renderCharts(selectedGender);
});
