"""
Alpha-beta minimax search for the chess engine.
Scores are positive when white is better and negative when black is better.
"""

import random


CHECKMATE = 100000
STALEMATE = 0
DEPTH = 2

pieceScore = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}

knightScores = [
    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
    [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
    [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
    [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
    [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
    [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
    [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
]

bishopScores = [
    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
    [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
    [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
    [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
    [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
]

rookScores = [
    [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
    [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25],
]

queenScores = [
    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
]

pawnScores = [
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
    [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
    [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
    [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
    [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
    [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
    [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
]

piecePositionScores = {
    'N': knightScores,
    'B': bishopScores,
    'R': rookScores,
    'Q': queenScores,
    'p': pawnScores,
}


def findRandomMove(validMoves):
    return random.choice(validMoves) if validMoves else None


def findBestMove(gs, validMoves, depth=DEPTH):
    """Return the best move found by negamax minimax with alpha-beta pruning."""
    if not validMoves:
        return None

    bestMove = None
    random.shuffle(validMoves)
    validMoves.sort(key=moveScoreGuess, reverse=True)
    rootDepth = depth

    def negamaxAlphaBeta(moves, currentDepth, alpha, beta, turnMultiplier):
        nonlocal bestMove

        if currentDepth == 0 or not moves:
            return turnMultiplier * scoreBoard(gs)

        maxScore = -CHECKMATE
        for move in moves:
            gs.makemove(move)
            nextMoves = gs.getValidMoves()
            nextMoves.sort(key=moveScoreGuess, reverse=True)
            score = -negamaxAlphaBeta(nextMoves, currentDepth - 1, -beta, -alpha, -turnMultiplier)
            gs.undomove()

            if score > maxScore:
                maxScore = score
                if currentDepth == rootDepth:
                    bestMove = move
            alpha = max(alpha, maxScore)
            if alpha >= beta:
                break

        return maxScore

    turnMultiplier = 1 if gs.whiteToMove else -1
    negamaxAlphaBeta(validMoves, depth, -CHECKMATE, CHECKMATE, turnMultiplier)
    return bestMove if bestMove is not None else findRandomMove(validMoves)


def moveScoreGuess(move):
    """Cheap move ordering so alpha-beta gets useful cutoffs earlier."""
    score = 0
    if move.pieceCaptured != '--':
        score += 10 * pieceScore[move.pieceCaptured[1]] - pieceScore[move.pieceMoved[1]]
    if move.isPawnPromotion:
        score += pieceScore['Q']
    return score


def scoreBoard(gs):
    if gs.checkMate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    if gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square == '--':
                continue

            piecePositionScore = 0
            piece = square[1]
            if piece != 'K':
                scoreTable = piecePositionScores[piece]
                piecePositionScore = scoreTable[row][col] if square[0] == 'w' else scoreTable[7-row][col]

            pieceValue = pieceScore[piece] + piecePositionScore
            score += pieceValue if square[0] == 'w' else -pieceValue

    return score
