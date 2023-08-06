


## pip install GitEdit


 ```python
    from editfile.util import createContent,m
    algebra = [
    m("a^2-b^2 = (a-b)(a\dotplus{b})"),
    m("\displaystyle x = \\frac{-b\pm\sqrt{b^2-4ac}}{2a}")
    ]
    tri = [
     m("sin\\theta")
    ]
    integral = [
    m("\displaystyle \int_0^2{x^2}dx")
    ]
    diff = [
     m("x^2 \\frac{dy}{dx}")
    ]
    prob = [
     m("\sigma^2")
    ]

topic = ["Mathematics",
            ["1. Algebra",algebra,
            "2. Trigonometry",tri,
            "3. Integral",integral,
             "4. Differentiation",diff,"5. Propability",prob],
           "Physics",["1. Quantum","2. Wave motion","3. Heat and Thermodynamics","4. Optics","5. Semiconductor"],
            "Chemistry",[
              "1. Periodic table",
              "2. Inorganic",
              "3. Organic"
             ]
          ]


createContent("test.md",expandColor="blue",data=topic)





 ```

# Output

##  View in test.md file


<details style="color:blue;"><summary style="color:blue;"><span style="color:black;">Mathematics</span></summary><ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">1. Algebra</span></summary><ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;"><img src="https://render.githubusercontent.com/render/math?math=a^2-b^2 = (a-b)(a\dotplus{b})"></span></summary></details><details style="color:blue;"><summary style="color:blue;"><span style="color:black;"><img src="https://render.githubusercontent.com/render/math?math=\displaystyle x = \frac{-b\pm\sqrt{b^2-4ac}}{2a}"></span></summary></details></details></ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">2. Trigonometry</span></summary><ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;"><img src="https://render.githubusercontent.com/render/math?math=sin\theta"></span></summary></details></details></ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">3. Integral</span></summary><ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;"><img src="https://render.githubusercontent.com/render/math?math=\displaystyle \int_0^2{x^2}dx"></span></summary></details></details></ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">4. Differentiation</span></summary><ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;"><img src="https://render.githubusercontent.com/render/math?math=x^2 \frac{dy}{dx}"></span></summary></details></details></ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">5. Propability</span></summary><ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;"><img src="https://render.githubusercontent.com/render/math?math=\sigma^2"></span></summary></details></details></ul></details></ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">Physics</span></summary><ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">1. Quantum</span></summary></details><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">2. Wave motion</span></summary></details><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">3. Heat and Thermodynamics</span></summary></details><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">4. Optics</span></summary></details><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">5. Semiconductor</span></summary></details></details></ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">Chemistry</span></summary><ul><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">1. Periodic table</span></summary></details><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">2. Inorganic</span></summary></details><details style="color:blue;"><summary style="color:blue;"><span style="color:black;">3. Organic</span></summary></details></details></ul>


[![Watch the video](https://img.youtube.com/vi/y-oH7KRYbCM/hqdefault.jpg)](https://www.youtube.com/watch?v=y-oH7KRYbCM)

