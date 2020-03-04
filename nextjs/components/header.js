import React from 'react'
import Link from 'next/link'

const menus = [
  { title: "foo" },
  { title: "baz" },
  { title: "bar" }
]

class Header extends React.Component {
  render() {
    return (
      <div>
        <div>
          <Link href="/">
            <a>index</a>
          </Link>
        </div>
        {menus.map((menu) => {
          return (
            <div>
              <Link href={`/post/${ menu.title }`}>
                <a>{ menu.title }</a>
              </Link>
            </div>
          )
        })}
      </div>
    )
  }
}

export default Header

