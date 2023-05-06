import React from 'react';

const PhotoDetectForm = ({ file, handleFileChange, handleUploadClick, image, report, error}) => (
  <div className="field field--wide">
    <input name="photo" type="file" onChange={handleFileChange} />

    <hr />

    <button onClick={handleUploadClick}>Upload</button>
    <div>
    {
      Object.keys(report).map((key, index) => {
        return (
          <div key={index}>
            <h3>
              {key}: {report[key]}
            </h3>
            <hr />
          </div>
        );
      })
    }
    </div>
    <div>
      <img src={image} width="100%"/>
    </div>
  </div>
);

export const PhotoDetect = () => {
  const [file, setFile] = React.useState("");
  const [error, setError] = React.useState();
  const [image, setImage] = React.useState("");
  const [report, setReport] = React.useState([]);
  
  const handleFileChange = (e) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUploadClick = () => {
    if (!file) {
      console.error("file missing")
      return;
    }

    // 👇 Uploading the file using the fetch API to the server
    fetch('http://localhost:5000/api/photo/detect', {
      method: 'POST',
      body: file,
    })
      .then((res) => {
        res.json().then(detection => {
          setReport(detection.report);
          setImage('http://localhost:5000/image?path=' + detection.path);
        });
      })
      .then((data) => {})
      .catch((err) => console.error(err));
  };

  return (
    <PhotoDetectForm
        file={file}
        error={error}
        handleFileChange={handleFileChange}
        handleUploadClick={handleUploadClick}
        image={image}
        report={report}
      />
  );
};

PhotoDetect.title = "PhotoDetect";
PhotoDetect.path = "/";
