graph [
  name "grid_2d_graph"
  node [
    id 0
    label "Keithside"
    switch "R"
  ]
  node [
    id 1
    label "Martinezstad"
    switch "R"
  ]
  node [
    id 2
    label "Harrisbury"
    switch "R"
  ]
  node [
    id 3
    label "West Ruben"
    switch "L"
  ]
  node [
    id 4
    label "Larryburgh"
    switch "L"
  ]
  node [
    id 5
    label "South Patricia"
    switch "R"
  ]
  edge [
    source 0
    target 4
    L1 "L"
    V1 "Keithside"
    V2 "Larryburgh"
    L2 "O"
  ]
  edge [
    source 0
    target 5
    L1 "R"
    V1 "Keithside"
    V2 "South Patricia"
    L2 "L"
  ]
  edge [
    source 0
    target 2
    L1 "O"
    V1 "Keithside"
    V2 "Harrisbury"
    L2 "O"
  ]
  edge [
    source 1
    target 2
    L1 "L"
    V1 "Martinezstad"
    V2 "Harrisbury"
    L2 "R"
  ]
  edge [
    source 1
    target 4
    L1 "O"
    V1 "Martinezstad"
    V2 "Larryburgh"
    L2 "L"
  ]
  edge [
    source 1
    target 3
    L1 "R"
    V1 "Martinezstad"
    V2 "West Ruben"
    L2 "R"
  ]
  edge [
    source 2
    target 3
    L1 "L"
    V1 "Harrisbury"
    V2 "West Ruben"
    L2 "O"
  ]
  edge [
    source 3
    target 5
    L1 "L"
    V1 "West Ruben"
    V2 "South Patricia"
    L2 "R"
  ]
  edge [
    source 4
    target 5
    L1 "R"
    V1 "Larryburgh"
    V2 "South Patricia"
    L2 "O"
  ]
]
