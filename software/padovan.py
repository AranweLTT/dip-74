def padovan_seq(index:int, m:int):
    # Initialize the Lucas sequence
    tempSeq = [3, 0, 2]

    # Calculate subsequent terms
    for i in range(3, index + 1):
        nextTerm = (tempSeq[i - 2] + tempSeq[i - 3])%m
        tempSeq.append(nextTerm)

    return tempSeq


def guess_seq_len(seq)->int:
    guess = 1
    max_len = int(round(len(seq) / 2))
    for x in range(2, max_len):
        if seq[0:x] == seq[x:2*x] :
            return x
    return guess


if __name__ == "__main__":
    maxlen = 0
    maxindex = 0
    for m in range(1, 17):
        mySeq = padovan_seq(2**10, m)
        seqlen = guess_seq_len(mySeq)
        print(f"m={m} seqlen: {seqlen}")
        if seqlen > maxlen:
            maxlen = seqlen
            maxindex = m

    print(f"\nmaxlen={maxlen} settings: {maxindex}")
    print(padovan_seq(maxlen+2, maxindex))
