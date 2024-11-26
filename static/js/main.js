// static/js/main.js

document
  .getElementById("workout-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const goal = document.getElementById("goal").value;
    const equipment = document.getElementById("equipment").value;
    const time = parseInt(document.getElementById("time").value);

    const response = await fetch("/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ goal, equipment, time }),
    });

    const recommendations = await response.json();
    const recommendationsDiv = document.getElementById("recommendations");
    recommendationsDiv.innerHTML =
      '<h2 class="text-2xl font-semibold">Recommended Workouts:</h2>';

    recommendations.forEach((exercise) => {
      recommendationsDiv.innerHTML += `
        <div class="bg-gray-200 p-4 mt-4 rounded">
          <h3 class="font-semibold">${exercise.name}</h3>
          <p>Muscle: ${exercise.muscle}</p>
          <p>Duration: ${exercise.duration} minutes</p>
        </div>
      `;
    });
  });

let currentStep = 1; // Tracks the current step
const totalSteps = 5; // Total number of steps

// Function to update the progress bar
function updateProgressBar() {
  const progress = (currentStep / totalSteps) * 100;
  document.getElementById("progress-bar").style.width = progress + "%";
}

// Function to move to the next step
function nextStep(step) {
  const currentStepDiv = document.getElementById(`step-${step}`);
  const nextStepDiv = document.getElementById(`step-${step + 1}`);

  // Hide the current step and show the next step
  currentStepDiv.style.display = "none";
  nextStepDiv.style.display = "block";

  currentStep++;
  updateProgressBar();
}

// Function to move to the previous step
function previousStep(step) {
  const currentStepDiv = document.getElementById(`step-${step}`);
  const previousStepDiv = document.getElementById(`step-${step - 1}`);

  // Hide the current step and show the previous step
  currentStepDiv.style.display = "none";
  previousStepDiv.style.display = "block";

  currentStep--;
  updateProgressBar();
}

// Function to handle selecting an option
function selectOption(step, value) {
  // Remove "selected" class from all buttons in the current step
  const buttons = document.querySelectorAll(`#step-${currentStep} .big-button`);
  buttons.forEach((button) => button.classList.remove("selected"));

  // Add "selected" class to the clicked button
  const selectedButton = document.querySelector(
    `#step-${currentStep} .big-button[onclick*="${value}"]`
  );
  selectedButton.classList.add("selected");

  // Store the selected value (you can handle it here, e.g., store in form or variable)
  document.getElementById(step).value = value;
}

// Initial progress bar setup
updateProgressBar();
