graph [
  name "grid_2d_graph"
  node [
    id 0
    label "Blevinsfurt"
    sw "L"
  ]
  node [
    id 1
    label "Jonesview"
    sw "L"
  ]
  node [
    id 2
    label "Kingburgh"
    sw "R"
  ]
  node [
    id 3
    label "Kyleburgh"
    sw "L"
  ]
  node [
    id 4
    label "Herbertview"
    sw "L"
  ]
  node [
    id 5
    label "Lisabury"
    sw "L"
  ]
  edge [
    source 0
    target 1
    Blevinsfurt "L"
    Jonesview "R"
  ]
  edge [
    source 0
    target 3
    Blevinsfurt "O"
    Kyleburgh "L"
  ]
  edge [
    source 0
    target 2
    Blevinsfurt "R"
    Kingburgh "L"
  ]
  edge [
    source 1
    target 4
    Jonesview "L"
    Herbertview "L"
  ]
  edge [
    source 1
    target 5
    Jonesview "O"
    Lisabury "L"
  ]
  edge [
    source 2
    target 4
    Kingburgh "R"
    Herbertview "O"
  ]
  edge [
    source 2
    target 3
    Kingburgh "O"
    Kyleburgh "R"
  ]
  edge [
    source 3
    target 5
    Kyleburgh "O"
    Lisabury "O"
  ]
  edge [
    source 4
    target 5
    Herbertview "R"
    Lisabury "R"
  ]
]
