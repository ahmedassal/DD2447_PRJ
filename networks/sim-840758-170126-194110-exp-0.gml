graph [
  name "grid_2d_graph"
  node [
    id 0
    label "Biancashire"
    sw "R"
  ]
  node [
    id 1
    label "West Christopher"
    sw "R"
  ]
  node [
    id 2
    label "South Christopher"
    sw "L"
  ]
  node [
    id 3
    label "Ortegamouth"
    sw "R"
  ]
  node [
    id 4
    label "North Johnmouth"
    sw "R"
  ]
  node [
    id 5
    label "East Lisa"
    sw "R"
  ]
  edge [
    source 0
    target 3
    Ortegamouth "L"
    Biancashire "O"
  ]
  edge [
    source 0
    target 5
    Biancashire "L"
