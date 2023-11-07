let fileInput = document.querySelector(".default-file-input");
let dragDropText = document.querySelector(".dynamic-message");


fileInput.addEventListener("click", () => {
	fileInput.value = '';
	console.log(fileInput.value);
});

fileInput.addEventListener("change", e => {
    let filename = fileInput.value
    filename = filename.replaceAll("\\","/").split("/")
    filename = filename.reverse()
    console.log(" > " + filename[0]);
    // uploadIcon.innerHTML = 'check_circle';
    dragDropText.innerHTML = 'File ' +(filename[0])+ ' Successfully!';
    document.querySelector(".label").innerHTML = `drag & drop or <span class="browse-files"> <input type="file" class="default-file-input" style=""/> <span class="browse-files-text" style="top: 0;"> browse file</span></span>`;
    uploadButton.innerHTML = `Upload`;
    fileName.innerHTML = fileInput.files[0].name;
    fileSize.innerHTML = (fileInput.files[0].size / 1024).toFixed(1) + " KB";
    uploadedFile.style.cssText = "display: flex;";
    progressBar.style.width = 0;
    fileFlag = 0;
});
