package product.product_services;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class ProductController {

    @RequestMapping(value="/", method=RequestMethod.GET)
    
    public String GetHello(){
        return "Hello from Spring Boot";
    }
}
