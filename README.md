<h1 align="center">Welcome to Magneto Hiring 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <img alt="Coverage" src="https://img.shields.io/badge/coverage-90%25-gren.svg?cacheSeconds=2592000" />
</p>

> Magneto's platform for recruiting mutants to fight the X-Men based on DNA. Using **lambda** powers to get the power!

## Stack

### Build with

* Python
* AWS Lambdas Serverless

## Demo Endpoint

### Create Mutant

#### Url: https://dd1fn7zy0i.execute-api.us-east-1.amazonaws.com/dev/mutant

This is a **POST** method

##### Human DNA

```json

{
  "dna": [
    "ATGCAA",
    "TGCTGA",
    "CAAACT",
    "ATGCAG",
    "TGCTGA",
    "CATGCT"
  ]
}

```

##### Mutant DNA HORIZONTAL

```json

{
  "dna": [
    "TTTGTA",
    "ACGTAT",
    "CGTATA",
    "GTATAC",
    "TATACG",
    "ATACGT"
  ]
}

```

##### Mutant DNA VERTICAL

```json

{
  "dna": [
    "ATGCAT",
    "TGCATT",
    "GCATAT",
    "CATATT",
    "ATATGC",
    "TATGCA"
  ]
}

```

##### Mutant DNA DIAGONALS

```json

{
  "dna": [
    "ATGCAA",
    "TACTGA",
    "CAAACT",
    "ATGCAG",
    "TGCTAA",
    "CATGCT"
  ]
}

```

##### Wrong DNA bad dna array size

```json

{
  "dna": [
    "ATGCGA",
    "CAGTGC",
    "TTATGT",
    "AGAAGG",
    "CCCCTA"
  ]
}

```

##### Wrong DNA bad dna letters

```json

{
  "dna": [
    "ATGCGA",
    "CAGTGC",
    "TTITGT",
    "AGAANG",
    "CCCCTA",
    "AGAAGG"
  ]
}

```

##### Wrong DNA bad dna elements size

```json

{
  "dna": [
    "ATGCGA",
    "CAGTGC",
    "TTATGT",
    "AGAAGG",
    "CCCCTA",
    "TCACT"
  ]
}

```

### Get Stats

#### Url: https://dd1fn7zy0i.execute-api.us-east-1.amazonaws.com/dev/stats

This is a **GET** method

## Install

```sh
npm run install:all
```

## Commands to run

```sh
sls offline
```

## Run tests

```sh
coverage run -m pytest tests.py
```

## Author

👤 **Fabio Garcia Sanchez**

* Github: [@fabgarsan](https://github.com/fabgarsan)
* LinkedIn: [@fabgarsan](https://linkedin.com/in/fabgarsan)

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_