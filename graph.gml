graph [
  name "grid_graph([3, 3])"
  node [
    id 0
    label "Sandersberg"
    switch "R"
  ]
  node [
    id 1
    label "West Amber"
    switch "R"
  ]
  node [
    id 2
    label "Laurenton"
    switch "R"
  ]
  node [
    id 3
    label "Port Monicafurt"
    switch "L"
  ]
  node [
    id 4
    label "Frederickbury"
    switch "L"
  ]
  node [
    id 5
    label "New William"
    switch "L"
  ]
  edge [
    source 0
    target 2
    label2 "L"
    label1 "R"
  ]
  edge [
    source 0
    target 4
    label2 "R"
    label1 "O"
  ]
  edge [
    source 0
    target 3
    label2 "O"
    label1 "L"
  ]
  edge [
    source 1
    target 3
    label2 "R"
    label1 "R"
  ]
  edge [
    source 1
    target 4
    label2 "L"
    label1 "L"
  ]
  edge [
    source 1
    target 5
    label2 "O"
    label1 "O"
  ]
  edge [
    source 2
    target 4
    label2 "O"
    label1 "R"
  ]
  edge [
    source 2
    target 5
    label2 "L"
    label1 "?"
  ]
  edge [
    source 3
    target 5
    label2 "?"
    label1 "L"
  ]
]
