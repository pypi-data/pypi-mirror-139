from pyfyre.widgets import *

class Header(Container):
    def __init__(self):

        _nav_items = [
            ["Documentation", "https://pyfyre.gitbook.io/docs/"],
            ["Playground", "/playground"],
            # ["Cookbook", "/"]
        ]

        def nav_items(i):
            return Link(
                className="block py-2 pr-4 pl-3 text-base text-black md:bg-transparent md:text-black md:p-0 cursor-pointer",
                textContent=_nav_items[i][0],
                to=_nav_items[i][1],
                external=True if "https" in _nav_items[i][1] else False
            )

        super().__init__(
            className = "bg-white border-gray-200 px-2 sm:px-4 py-2.5 border-b-2 sticky top-0",
            children = [
                Container(
                    className="flex flex-wrap justify-between items-center mx-auto",
                    children=[
                        Container(
                            className="flex",
                            children=[
                                Image(
                                    className="w-10",
                                    src="https://scontent.fmnl13-1.fna.fbcdn.net/v/t1.6435-9/164540820_110370211141719_22088476788963606_n.jpg?_nc_cat=104&ccb=1-5&_nc_sid=09cbfe&_nc_ohc=Qg8QkUIRCLIAX9ll7Gs&tn=LaPlocOuMCICDrK8&_nc_ht=scontent.fmnl13-1.fna&oh=00_AT8iHOF8SKnb4kNw1oUH24roDJ3w7HQdux72Jdf2850yrg&oe=62169F42"
                                ),
                            ]
                        ),
                        Container(
                            className="flex items-center space-x-5",
                            children=[
                                ListBuilder(
                                    className="invisible flex space-x-5 lg:visible",
                                    count=len(_nav_items),
                                    builder=nav_items
                                ),
                                Link(
                                    className="text-white cursor-pointer font-black bg-[#fab327] focus:ring-4 font-medium rounded-3xl text-sm px-5 py-2.5 text-center mr-3 md:mr-0",
                                    textContent="Get Started",
                                    to="https://pyfyre.gitbook.io/docs/quick-start",
                                    external=True
                                )
                            ]
                        ),
                    ]
                )
            ]
        )