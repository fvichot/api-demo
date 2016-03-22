package main
import (
    "github.com/gin-gonic/gin"
    "net/http"
)


/* Too lazy to connect to a DB, let's hardcode some values */
var secrets = gin.H{
    "bob":    gin.H{"email": "foo@bar.com", "phone": "123433"},
    "admin":  gin.H{"email": "austin@example.com", "phone": "666"},
    "lena":   gin.H{"email": "lena@guapa.com", "phone": "523443"},
}


func foobar(c *gin.Context) {
    c.String(http.StatusOK, "foobar called")
}



func main() {
    router := gin.Default()

    // This handler will match /user/john but will not match neither /user/ or /user
    router.GET("/user/:name", func(c *gin.Context) {
        name := c.Param("name")
        c.String(http.StatusOK, "Hello %s", name)
    })

    // However, this one will match /user/john/ and also /user/john/send
    // If no other routers match /user/john, it will redirect to /user/john/
    router.GET("/user/:name/*action", func(c *gin.Context) {
        name := c.Param("name")
        action := c.Param("action")
        message := name + " is " + action
        c.String(http.StatusOK, message)
    })

    // Simple group: v1
    v1 := router.Group("/v1")
    {
        v1.GET("/test", foobar)
    }

    // Simple group: v2
    v2 := router.Group("/v2")
    {
        v2.GET("/testage", foobar)
    }

    router.Run(":8080")
}
