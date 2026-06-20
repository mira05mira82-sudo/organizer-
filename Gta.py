OpenCity/
│
├── Assets/
│   ├── Scripts/
│   │   ├── PlayerController.cs
│   │   ├── CarController.cs
│   │   ├── CameraFollow.cs
│   │   └── GameManager.cs
│   │
│   ├── Models/
│   ├── Materials/
│   ├── Prefabs/
│   ├── Audio/
│   └── Scenes/
│       └── City.unity
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float speed = 6f;
    public float jumpForce = 7f;

    Rigidbody rb;
    bool grounded = true;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void Update()
    {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");

        Vector3 move = transform.forward * v + transform.right * h;
        transform.position += move * speed * Time.deltaTime;

        if(Input.GetKeyDown(KeyCode.Space) && grounded)
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
            grounded = false;
        }
    }

    void OnCollisionEnter(Collision c)
    {
        grounded = true;
    }
}
using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    public Transform target;
    public Vector3 offset;

    void LateUpdate()
    {
        transform.position = target.position + offset;
        transform.LookAt(target);
    }
}
