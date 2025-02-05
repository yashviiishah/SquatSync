using UnityEngine;
using TMPro;  // Import the TextMeshPro namespace

public class GameTimer : MonoBehaviour
{
    public float timeRemaining = 60f; // Set the timer for 60 seconds
    public bool timerIsRunning = false;
    public TextMeshProUGUI timerText;  // Reference to the TextMeshProUGUI component

    void Start()
    {
        // Start the timer
        timerIsRunning = true;
    }

    void Update()
    {
        if (timerIsRunning)
        {
            if (timeRemaining > 0)
            {
                // Decrease the time remaining
                timeRemaining -= Time.deltaTime;
                // Update the timer text in the UI
                UpdateTimerDisplay(timeRemaining);
            }
            else
            {
                // Timer has reached zero, exit the game
                timeRemaining = 0;
                timerIsRunning = false;
                ExitGame();
            }
        }
    }

    // Update the UI TextMeshPro to display the remaining time
    void UpdateTimerDisplay(float currentTime)
    {
        currentTime += 1;  // To display the time in a better format
        float minutes = Mathf.FloorToInt(currentTime / 60);
        float seconds = Mathf.FloorToInt(currentTime % 60);

        // Update the TextMeshProUGUI component to show the time remaining (e.g., 00:59)
        timerText.text = string.Format(" Time left - {0:00}:{1:00}", minutes, seconds);
    }

    // Exit the game when time runs out
    void ExitGame()
    {
        Debug.Log("Time's up! Exiting the game...");
#if UNITY_EDITOR
            // If running in the Unity editor, stop play mode
            UnityEditor.EditorApplication.isPlaying = false;
#else
        // If running in a built game, quit the application
        Application.Quit();
#endif
    }
}
