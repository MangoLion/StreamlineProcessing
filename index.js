const fs = require('fs');
const path = require('path');

const express = require('express');
const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload');
const session = require('express-session');

const app = express();
const port = 3000;

// Configure body-parser middleware
app.use(express.static('public'))
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

// Configure file upload middleware
app.use(fileUpload());

// Configure session middleware
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true
}));

// Serve the HTML file with the form
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Handle form submission
app.post('/submit', (req, res) => {
  const numberOfStreamlines = req.body.numberOfStreamlines;
  const stepSize = req.body.stepSize;
  const maxLength = req.body.maxLength;
  // Store the uploaded file in session
  if (req.files && req.files.dataset) {
    const dataset = req.files.dataset.data.toString('utf8');
    
    // Define the file path
    const filePath = path.join(__dirname, 'uploads', req.files.dataset.name);

    // Write the file
    fs.writeFile(filePath, dataset, (err) => {
      if (err) {
        console.error('Failed to write file:', err);
        res.status(500).send('Server error');
      } else {
        console.log('File saved successfully');
      }
    });

    req.session.datasetContent = dataset;

    //example: use this to retrieve the filepath later when you get it working
    //req.session.datasetPath = filePath;
  }

  // Redirect to the result page
  res.redirect(`/result?numberOfStreamlines=${numberOfStreamlines}&stepSize=${stepSize}&maxLength=${maxLength}`);
});

app.get('/result', (req, res) => {
  const numberOfStreamlines = req.query.numberOfStreamlines;
  const stepSize = req.query.stepSize;
  const maxLength = req.query.maxLength;
  

  /*------------CALL PYTHON SCRIPT HERE--------------*/
  //example command: python streamlines.py --file_path bernard3D.vtk --output_path out.csv --num_streamlines 24 --step_size 0.1 --max_propagation 5

  /*-----------*/

  //datasetContent should be the contents of the streamlines csv file, surrounded by the ` character, example below:
  const datasetContent ="`" + req.session.datasetContent + "`";
  delete req.session.datasetContent; // Clear the stored session data

  res.render('result', { 
    numberOfStreamlines: numberOfStreamlines, 
    stepSize: stepSize, 
    maxLength: maxLength, 
    datasetContent: datasetContent 
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
