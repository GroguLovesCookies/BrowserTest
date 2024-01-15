# Charm
A browser with (planned) easy modding, privacy, AI access, exclusive HTML/CSS Features, and more. Very much in development.

## HTML/CSS Features
### Custom Attributes
```
<html foo="bar">
    .
    .
    .
</html>
```

### Targeted Selectors
For the HTML file
```
<html>
    <body>
        <p id="p1">
            <a id="sub-p1">
            </a>
        </p>
        <div id="div1">
        </div>
        <p id="p2>
        </p>
        <a></a>
    </body>
    <p>
    </p>
</html>
```

The CSS Selector `p + div` selects all div elements preceded directly by p elements, i.e. `div#div1`. The *targeted* selector `&p + div` selects all p elements with a div element immediately after, i.e, `p#p1`

The CSS selector `body > p > a` selects `a#sub-p1`, but the targeted selector `body > &p > a` selects the element `p#p1`.

