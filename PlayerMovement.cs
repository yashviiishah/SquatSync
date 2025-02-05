using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    // This reference will be set in the UDPReceiver
    public static bool movePlayer = false;

    void Update()
    {
        // Move the cube by 1 unit in the Y direction when moveCube is true
        if (movePlayer)
        {
            transform.Translate(Vector3.forward * 1.0f);  // Move 1 unit up
            movePlayer = false;  // Reset the moveCube flag after moving
        }
    }
}
