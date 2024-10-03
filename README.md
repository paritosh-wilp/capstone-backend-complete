# capstone-backend-complete
This is the complete django backend of bookAslot capstone project for BITS PILANI wilp course.

This project supports following apis . 

    business/signup/', BusinessSignupView.as_view(), name='business-signup'),customer login--> signup for buisiness 
    business/login/', BusinessLoginView.as_view(), name='business-login'), --> businsess login
    customer/signup/', CustomerSignupView.as_view(), name='customer-signup'),  --> signup for customers
    customer/login/', CustomerLoginView.as_view(), name='customer-login'), --> customer login
    sessions/', SessionListCreateView.as_view(), name='session-list-create'), --> get all session , create new sessions [ will be used by buisiness admin]
    sessions/<int:pk>/', SessionDetailView.as_view(), name='session-detail'), --> update any session by session id 
    sessions/business/list/<int:business_id>/', SessionByBusinessView.as_view(), name='list-session-by-business'), --> list all sessions for buisiness id 
    sessions/business/<int:business_id>/', UpdateSessionByBusinessView.as_view(), name='update-sessions-by-business'), --> update all session for 1 buisiness < all session cancelled etc >
    sessions/business/<int:business_id>/<int:session_id>/', UpdateSessionByBusinessView.as_view(), name='update-session-by-business'),  --> update a particular session of buisiness by session id < marking complete etc>
    sessions/customer/list/<int:customer_id>/', SessionByCustomerView.as_view(), name='list-session-by-customer'), --> list all sessions for customerid
    sessions/customer/<int:customer_id>/<int:session_id>/', UpdateSessionByCustomerView.as_view(), name='update-session-by-customer'),  --> update a particular session of customer by session id < booking/cancelling a session>
]
