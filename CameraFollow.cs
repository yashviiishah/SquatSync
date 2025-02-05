using UnityEngine;


public class CameraFollow : MonoBehaviour
{
    public Transform target;  // The target object to follow
    public Vector3 offset;    // Offset distance between the camera and the target

    void LateUpdate()
    {
        if (target != null)
        {
            // Move the camera to maintain the offset directly from the player's current position
            transform.position = target.position + offset;

            // Make the camera look at the target (optional for fixed focus)
            transform.LookAt(target);
        }
    }
}
