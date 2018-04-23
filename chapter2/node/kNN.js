const fs = require('fs')
const path = require('path')
const numbers = require('numbers')
function getMatrixs(myPath) {
    let dirPath = path.resolve(myPath)
    console.log(dirPath)
    let result
    result = fs.readdirSync(dirPath)
    // console.log(result)
    return result.map((fileName, index) => {
        let label = Number(fileName.split('_')[0])
        let filePath = path.join(dirPath, fileName)
        var content = fs.readFileSync(filePath, 'utf-8')
        matrix = content.replace(/\s|\n/g,'').split(/\n|\t|r/).map((item) => {
            let r = []
            item.split('').forEach((bit) => {
                r.push(parseInt(bit))
            })
            return r
        })
        // console.log('matrix--->' + matrix)
        return {
            label,
            matrix
        }
    })
}
function compareMatrix (matrixA, matrixB) {
    let dist = numbers.matrix.subtraction(matrixA, matrixB)
    let sum = 0
    const sonSum = function (array) {
        if (typeof array === 'number') {
            sum += array*array
        } else {
            array.forEach((item) => {
                sonSum(item)
            })
        }
    }
    sonSum(dist)
    return sum
}
function kNearestNeighbor (testdata, dataSet, k) {
    let len = dataSet.lenght
    let diffMat
    let map = {}
    let result, max = 0
    let sortedDataSet = dataSet.sort((item1, item2) => {
        let deviation1 = compareMatrix(testdata, item1.matrix)
        let deviation2 = compareMatrix(testdata, item2.matrix)
        return deviation1 - deviation2
    })
    // console.log('sortedDataSet---->' + sortedDataSet)
    for (let i = 0; i < k; i ++) {
        map[sortedDataSet[i].label] = map.hasOwnProperty(sortedDataSet[i].label) ? (map[sortedDataSet[i].label] + 1) : 1
    }
    
    for (let p in map) {
        if (map[p] > max) {
            result = p
            max = map[p]
        }
    }
    return result
}
let testData = getMatrixs('./chapter2/digits/testDigits')
let data = getMatrixs('./chapter2/digits/trainingDigits')
// console.log('Predict result: ' + kNearestNeighbor(testData[90].matrix, data, 3))
let total = testData.length
let rightCount = 0
testData.forEach((item) => {
    let predict = kNearestNeighbor(item.matrix, data, 3)
    if (predict == item.label) {
        rightCount ++
    }
    console.log('Predict result: ' + predict + ', real value:' + item.label)
    console.log('Total: ' + total + ', right count:' + rightCount)
})
console.log((rightCount/total*100).toFixed(2) + '% are right')
// var vector1 = [[1, 0, 0]]
// var vector2 = [[1, -1, 0]]
// // // console.log(numbers.matrix.subtraction(vector1, vector2))
// console.log(numbers.matrix.scalar(vector1, 3))
// console.log(compareMatrix(vector1, vector2))