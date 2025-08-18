const API_ENDPOINT = "/predict";

const imageUpload = document.getElementById("imageUpload");
const predictButton = document.getElementById("predictButton");
const resultText = document.getElementById("resultText");
const imagePreview = document.getElementById("imagePreview");
const sampleDropdown = document.getElementById("sampleDropdown");
let uploadedFile = null;

sampleDropdown.addEventListener("change", (event) => {
  const selected = event.target.value;
  if (selected) {
    // show preview
    imagePreview.innerHTML = "";
    const img = document.createElement("img");
    img.src = `/static/sample_images/${selected}`;
    img.style.maxWidth = "300px";
    imagePreview.appendChild(img);
    resultText.innerText = "...";
    // fetch the image as a blob and set as uploadedFile
    fetch(img.src)
      .then((res) => res.blob())
      .then((blob) => {
        uploadedFile = new File([blob], selected, { type: blob.type });
      });
  } else {
    uploadedFile = null;
    imagePreview.innerHTML = "";
    resultText.innerText = "...";
  }
});

imageUpload.addEventListener("change", (event) => {
  // get the selected file
  uploadedFile = event.target.files[0];
  if (uploadedFile) {
    // clear previous preview
    imagePreview.innerHTML = "";
    // create an image element to show a preview
    const reader = new FileReader();
    reader.onload = function (e) {
      const img = document.createElement("img");
      img.src = e.target.result;
      img.style.maxWidth = "300px"; // preview size
      imagePreview.appendChild(img);
    };
    reader.readAsDataURL(uploadedFile);
    resultText.innerText = "...";
    // reset dropdown selection
    sampleDropdown.value = "";
  }
});

predictButton.addEventListener("click", async () => {
  if (!uploadedFile) {
    alert("Please select an image first!");
    return;
  }
  resultText.innerText = "Predicting...";
  // create a FormData object to send the file
  const formData = new FormData();
  formData.append("file", uploadedFile);

  try {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (data.error) {
      resultText.innerText = "Error: " + data.error;
    } else {
      resultText.innerText = `Prediction: ${data.prediction} (Confidence: ${(
        data.confidence * 100
      ).toFixed(2)}%)`;
    }
  } catch (err) {
    resultText.innerText = "Prediction failed.";
  }
});
