# %%
# install.packages("shiny")
library(shiny)
library(data.table)

# %% UI (FRONTEND)
ui <- shiny::fluidPage(
  titlePanel("Análisis de Pandeo de Soporte (Curva a)"),

  sidebarLayout(
    sidebarPanel(
      sliderInput(
        "A",
        "Área (cm²):",
        min = 10,
        max = 80,
        value = 20.4,
        step = 0.1
      ),
      sliderInput(
        "i",
        "Radio de giro i (cm):",
        min = 2,
        max = 10,
        value = 4.8,
        step = 0.1
      ),
      hr(),
      p(
        "Cálculo basado en CTE / Eurocódigo 3 para tubos de chapa simple conformados en caliente."
      )
    ),

    mainPanel(
      plotOutput("bucklePlot", height = "500px")
    )
  )
)

# --- SERVER (BACKEND) ---
server <- function(input, output) {
  # Pre-calculate the theoretical curve once using data.table for maximum speed
  dt_curve <- shiny::reactiveVal({
    lambdas <- seq(0.01, 3.0, length.out = 200)
    alpha <- 0.21
    Phis <- 0.5 * (1 + alpha * (lambdas - 0.2) + lambdas^2)
    chis <- 1 / (Phis + sqrt(pmax(0, Phis^2 - lambdas^2)))
    chis <- pmin(1.0, chis)
    data.table(lambda = lambdas, chi = chis)
  })

  # Reactively render the plot whenever inputs change
  output$bucklePlot <- shiny::renderPlot({
    # Static parameters
    L_k_mm <- 3.45 * 1000
    f_y <- 275
    E <- 210000
    alpha <- 0.21
    gamma_s <- 1.05
    N_Ed <- 490

    # Fetch slider inputs
    A_mm2 <- input$A * 100
    i_mm <- input$i * 10

    # Physics calculations
    I <- A_mm2 * (i_mm^2)
    N_cr <- (pi^2 * E * I) / (L_k_mm^2)
    lambda_bar <- sqrt((A_mm2 * f_y) / N_cr)

    Phi_pt <- 0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar^2)
    chi_pt <- min(1.0, 1 / (Phi_pt + sqrt(max(0, Phi_pt^2 - lambda_bar^2))))

    N_b_Rd <- chi_pt * A_mm2 * (f_y / gamma_s) / 1000

    # Determine result state
    is_passing <- N_b_Rd >= N_Ed
    punto_color <- ifelse(is_passing, "forestgreen", "red")
    estado <- ifelse(is_passing, "CUMPLE:", "NO CUMPLE:")
    texto_res <- sprintf("%s N_b,Rd = %.1f kN", estado, N_b_Rd)

    # Plotting using Base R graphics
    curve_data <- dt_curve()

    # Setup empty plot frame
    plot(
      curve_data$lambda,
      curve_data$chi,
      type = "n",
      xlab = expression(paste("Esbeltez Reducida (", bar(lambda), ")")),
      ylab = expression(paste("Coeficiente de Pandeo (", chi, ")")),
      xlim = c(0, 3.0),
      ylim = c(0, 1.1),
      xaxs = "i",
      yaxs = "i",
      bty = "l",
      cex.lab = 1.2
    )

    # Add grid
    grid(col = "lightgray", lty = "dotted")

    # Draw theoretical curve
    lines(curve_data$lambda, curve_data$chi, lwd = 2, col = "black")

    # Draw trial profile point
    points(lambda_bar, chi_pt, pch = 19, col = punto_color, cex = 2.5)

    # Add legend and results
    legend(
      "topright",
      legend = c("Curva a", "Perfil Trial"),
      col = c("black", punto_color),
      lwd = c(2, NA),
      pch = c(NA, 19),
      bty = "n",
      cex = 1.2
    )

    text(
      x = 0.1,
      y = 0.1,
      labels = texto_res,
      col = punto_color,
      pos = 4,
      font = 2,
      cex = 1.3
    )
  })
}

# %% Run the application
shiny::shinyApp(ui = ui, server = server)