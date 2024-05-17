console.log("simulation.js");

const canvasEl = document.getElementById("myCanvas");
const ctx = canvasEl.getContext("2d");
const canvasWidth = 500;
const canvasHeight = 500;

let numGrids = 100;
let colors = ["#123456", "#654321", "#FFFFFF", "orange"];
let squareSize = canvasWidth / numGrids;

let grid = generateGrid([numGrids, numGrids], 3);
let threshold = 3;
let states = 3;

// Interval in milliseconds
let interval = 200; 
let lastTime = 0;

document.addEventListener("keydown", (event) => {
    if (event.code === "Space") {
        grid = runSimulation(grid, threshold, states);
        fillGrid(grid);
    }
});

function startSimulation(timestamp) {
    if (timestamp - lastTime >= interval) {
        grid = runSimulation(grid, threshold, states);
        fillGrid(grid);
        lastTime = timestamp;
    }
    requestAnimationFrame(startSimulation);
}
requestAnimationFrame(startSimulation);

function generateGrid(size, states) {
    let rows = size[0];
    let cols = size[1];
    let grid = [];
    for (let i = 0; i < rows; i++) {
        let row = [];
        for (let j = 0; j < cols; j++) {
            row.push(getRandomInt(0, states - 1));
        }
        grid.push(row);
    }
    return grid;
}

function fillGrid(grid) {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    for (let i = 0; i < numGrids; i++) {
        for (let j = 0; j < numGrids; j++) {
            ctx.fillStyle = colors[grid[i][j]];
            ctx.fillRect(i * squareSize, j * squareSize, squareSize, squareSize);
        }
    }
}

function findMooreNeighbourhood(cell, grid) {
    let cellI = cell[0];
    let cellJ = cell[1];

    if (cellI >= grid.length || cellJ >= grid[0].length) {
        throw "error"
    }

    let minI = Math.max(0, cellI - 1);
    let minJ = Math.max(0, cellJ - 1);
    let maxI = Math.min(grid.length - 1, cellI + 1);
    let maxJ = Math.min(grid[0].length - 1, cellJ + 1);

    let neighbourhood = [];
    for (let i = minI; i <= maxI; i++) {
        for (let j = minJ; j <= maxJ; j++) {
            if (i !== cellI || j !== cellJ) {
                neighbourhood.push(grid[i][j]);
            }
        }
    }
    return neighbourhood;
}

function countMooreNeighbourhood(neighbourhood, states) {
    let tally = new Array(states).fill(0);
    neighbourhood.forEach(state => {
        tally[state]++;
    });
    return tally;
}

function calculateNewState(state, tally, threshold, states) {
    let newState;
    let opponent = (state + 1) % states;

    let count = tally[opponent];
    if (count >= threshold) {
        newState = opponent;
    } else {
        newState = state;
    }

    return newState;
}

function runSimulation(grid, threshold = 2, states = 3) {
    fillGrid(grid);

    let newGrid = [];
    for (let i = 0; i < grid.length; i++) {
        let newRow = [];
        for (let j = 0; j < grid[0].length; j++) {
            let neighbourhood = findMooreNeighbourhood([i, j], grid);
            let tally = countMooreNeighbourhood(neighbourhood, states);
            let newState = calculateNewState(grid[i][j], tally, threshold, states);

            newRow.push(newState);
        }

        newGrid.push(newRow);
    }

    return newGrid;
}

function getRandomInt(min = 0, max = 10) {
    const minCeiled = Math.ceil(min);
    const maxFloored = Math.floor(max);
    return Math.floor(Math.random() * (maxFloored - minCeiled + 1) + minCeiled); // The maximum is inclusive and the minimum is inclusive
}
