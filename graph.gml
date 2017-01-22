graph [
  name "grid_graph([3, 3])"
  node [
    id 0
    label "Port Theresaside"
    switch "L"
  ]
  node [
    id 1
    label "Port Sheilashire"
    switch "R"
  ]
  node [
    id 2
    label "Drakefurt"
    switch "L"
  ]
  node [
    id 3
    label "West Kimberly"
    switch "R"
  ]
  node [
    id 4
    label "Nicholasmouth"
    switch "R"
  ]
  node [
    id 5
    label "Lake Amanda"
    switch "L"
  ]
  edge [
    source 0
    target 1
    label1 "O"
    label2 "O"
  ]
  edge [
    source 0
    target 5
    label1 "L"
    label2 "R"
  ]
  edge [
    source 0
    target 3
    label1 "R"
    label2 "L"
  ]
  edge [
    source 1
    target 3
    label1 "L"
    label2 "?"
  ]
  edge [
    source 1
    target 2
    label1 "R"
    label2 "?"
  ]
  edge [
    source 2
    target 5
    label1 "R"
    label2 "O"
  ]
  edge [
    source 2
    target 4
    label1 "L"
    label2 "L"
  ]
  edge [
    source 3
    target 4
    label1 "R"
    label2 "?"
  ]
  edge [
    source 4
    target 5
    label1 "O"
    label2 "?"
  ]
]
